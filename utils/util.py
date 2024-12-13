from treys import Card


def print_table(player_names, cards):
    # Print the headers
    column_width = 15  # Set the column width
    header_format = "".join([f"{{:<{column_width}}}" for _ in player_names])
    # Print the headers
    print(header_format.format(*player_names))
    print(header_format.format(Card.int_to_pretty_str(cards)))

