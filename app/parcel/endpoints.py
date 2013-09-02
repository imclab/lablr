from flask import abort, request, jsonify
from flask.ext.restful import abort, Resource, reqparse
from werkzeug.exceptions import ClientDisconnected
import easypost
import decimal


parser = reqparse.RequestParser()
parser.add_argument('length', type=decimal.Decimal, location='json')
parser.add_argument('width', type=decimal.Decimal, location='json')
parser.add_argument('height', type=decimal.Decimal, location='json')
parser.add_argument('weight', type=decimal.Decimal, location='json')


class Parcel(Resource):

    def post(self):
        try:
            args = parser.parse_args()
            for key, value in args.iteritems():
                args[key] = value.quantize(decimal.Decimal(10) ** -1).normalize()
        except ClientDisconnected as e:
            abort(400, errorItem='parcel', message='Parcel info is not valid')

        to_address = easypost.Address.create(
            name="Foo Bar",
            street1="387 Townsend St",
            city="San Francisco",
            state="CA",
            zip="94107",
            phone="415-450-7890"
        )

        from_address = easypost.Address.create(
            name="John Smith",
            street1="388 Townsend St",
            city="San Francisco",
            state="CA",
            zip="94107",
            phone="415-459-7890"
        )

        # verify addresses
        try:
            #verified_from_address = from_address.verify()
            verified_from_address = from_address
        except easypost.Error as e:
            abort(400, errorItem='fromAddress', message='From address is not valid')
        if hasattr(verified_from_address, 'message'):
            # the from address is not invalid, but it has an issue
            pass

        try:
            #verified_to_address = to_address.verify()
            verified_to_address = to_address
        except easypost.Error as e:
            abort(400, errorItem='toAddress', message='To address is not valid')
        if hasattr(verified_to_address, 'message'):
            # the from address is not invalid, but it has an issue
            pass

        try:
            parcel = easypost.Parcel.create(
                length=args.get('length'),
                width=args.get('width'),
                height=args.get('height'),
                weight=args.get('weight')
            )
        except easypost.Error as e:
            abort(400, errorItem='parcel', message='Parcel info is not valid')

        # create shipment
        try:
            shipment = easypost.Shipment.create(
                to_address=verified_to_address,
                from_address=verified_from_address,
                parcel=parcel,
            )
        except easypost.Error as e:
            abort(400, errorItem='parcel', message='Error creating label, parcel may be too large')

        lowest_rate = shipment.lowest_rate()

        try:
            shipment.buy(rate=lowest_rate)
        except easypost.Error as e:
            abort(400, errorItem='parcel', message='Error creating label, please try again')

        return {
            'postageUrl': shipment.postage_label.label_url,
            'carrier': lowest_rate.carrier,
            'service': lowest_rate.service,
            'rate': lowest_rate.rate,
        }
