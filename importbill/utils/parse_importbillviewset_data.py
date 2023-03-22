def parse_data(data):
    def percentageOrRate(type, symbol, data):
        def convertIncrementType(type, value):
            if data[f"{type}Type"] == "%":
                discountAmount = (
                    value/100) * data["rate"] if type == "discount" else (value/100) * data["ourRate"]
                return discountAmount
            elif data[f"{type}Type"] == "Rs":
                discountAmount = (100*(value/data["quantity"])) / data["rate"] \
                    if type == "discount" else (value*100)/data["ourRate"]
                return discountAmount

        value = data["discount"] if type == "discount" else data["increment"]

        final_value = value / \
            data["quantity"] if symbol == "Rs" and type == "discount" else value

        return final_value if data[f"{type}Type"] == symbol else convertIncrementType(type, value)

    product_data = {
        "product_name": data["productName"],
        "in_stock": data["quantity"],
        "sales_unit": data["salesUnit"],
        "rate": data["rate"],
        "our_rate": data["ourRate"],
        "discount_percentage": percentageOrRate("discount", "%", data),
        "discount_rate": percentageOrRate("discount", "Rs", data),
        "increment_percentage": percentageOrRate("increment", "%", data),
        "increment_rate": percentageOrRate("increment", "Rs", data),
        "latest_bill_date": data["date"],
    }
    product_data["price"] = product_data["increment_rate"] + \
        product_data["our_rate"]
    bill_data = {
        "amount_in_kg": None if data["kg"] == 0 else data["kg"],
        "amount_in_pcs": data["quantity"],
        "total_price": data["buy"],
        "discount_percentage": percentageOrRate("discount", "%", data),
        "discount_rate": percentageOrRate("discount", "Rs", data),
        "rate": data["rate"],
        "our_rate": data["ourRate"],
        "import_date": data["date"]
    }

    final_data = {"product_data": product_data, "bill_data": bill_data}

    return final_data
