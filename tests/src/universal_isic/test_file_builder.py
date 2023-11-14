def test_build_data_from_hierarchical_csv():
    # With
    from universal_isic.file_builder import build_data_from_hierarchical_csv
    from io import StringIO

    expected_n_level = 4

    # When
    csv = StringIO(
        """
"A","Agriculture, forestry and fishing"
"01","Crop and animal production, hunting and related service activities"
"011","Growing of non-perennial crops"
"0111","Growing of cereals (except rice), leguminous crops and oil seeds"
"0112","Growing of rice"
"0113","Growing of vegetables and melons, roots and tubers"
"0114","Growing of sugar cane"
"0115","Growing of tobacco"
"0116","Growing of fibre crops"
"0119","Growing of other non-perennial crops"
"012","Growing of perennial crops"
"0121","Growing of grapes"
"0122","Growing of tropical and subtropical fruits"
"0123","Growing of citrus fruits"
"0124","Growing of pome fruits and stone fruits"
"0125","Growing of other tree and bush fruits and nuts"
"0126","Growing of oleaginous fruits"
"0127","Growing of beverage crops"
"0128","Growing of spices, aromatic, drug and pharmaceutical crops"
"0129","Growing of other perennial crops"
"013","Plant propagation"
                   """
    )
    (
        actual_n_level,
        actual_levels_dict,
        actual_mapping_dict,
    ) = build_data_from_hierarchical_csv(csv, header=None)

    # Then
    assert expected_n_level == actual_n_level
