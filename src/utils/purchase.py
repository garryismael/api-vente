def get_products_ids_not_found_in_db(products_ids: list[int], products_ids_in_db: list[tuple[int]]):
    products_not_found = []
    for id in products_ids:
        found = False
        for ids_in_db in products_ids_in_db:
            if id == ids_in_db[0]:
                found = True
                break
        if not found:
            products_not_found.append(id)
    return products_not_found
