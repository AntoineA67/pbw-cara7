import xrpl.wallet.wallet_generation
from util.json import read_data_from_car_json
import xrpl


# Scoring algorithm for cars either A, B, or C
def scoring():
    cars_data = read_data_from_car_json("../data/")

    def score_one_car(car_data):
        battery_health = car_data["batteryHealth"]
        total_kilometers = car_data["totalKilometers"]
        payment_default = car_data["leaseDetails"]["paymentDefault"]
        late_payment_months = car_data["leaseDetails"]["latePaymentMonths"]

        # Scoring criteria
        if (
            battery_health > 90
            and total_kilometers < 30000
            and not payment_default
            and late_payment_months < 2
        ):
            return "A"
        elif (
            80 <= battery_health <= 90
            and total_kilometers < 40000
            and late_payment_months < 4
        ):
            return "B"
        else:
            return "C"

    # Example usage
    car_scores = {
        filename: score_one_car(car_info) for filename, car_info in cars_data.items()
    }
    print(car_scores)


wallet = xrpl.wallet.(seed="snoPBr")
print(wallet.classic_address)


# TODO Tranching algorithm

# TODO Create 3 wallets (XRP)

# TODO Move NFTs to wallets according to scoring and tranching

# TODO Get list of investor, generate trustlines for each investor
