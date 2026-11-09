import argparse
import geopandas as gpd
import h3
import pandas as pd


def convert_to_h3(geojson_file, output_file, output_format, resolution):
    # Read the GeoJSON file using geopandas
    gdf = gpd.read_file(geojson_file)

    # Check if the geometry type is Point
    if gdf.geometry.type[0] != "Point":
        raise ValueError("Input data must contain point geometries only.")

    unique = False
    while not unique:
        # Convert each point to H3 hexagons at the resolution
        gdf["h3_hexagon"] = gdf.geometry.apply(
            lambda point: h3.geo_to_h3(point.y, point.x, resolution)
        )

        # Check if there are any duplicate H3 hexagons
        if gdf["h3_hexagon"].duplicated().any():
            # Increase the resolution to ensure unique hexagons
            resolution += 1
            if resolution > 15:
                print(
                    "Warning: Maximum resolution reached. Some hexagons may be duplicated."
                )
                break
            print(f"Duplicate hexagons found. Increasing resolution to {resolution}.")
        else:
            unique = True

    # Save the resulting data to the output file
    if output_format == "csv":
        # Create a DataFrame with h3_hexagon as the first column
        df = pd.DataFrame({"h3_hexagon": gdf["h3_hexagon"]})

        # Save the DataFrame to CSV
        df.to_csv(output_file, index=False)
    else:
        # Save the GeoDataFrame to GeoJSON
        gdf.to_file(output_file, driver="GeoJSON")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Convert GeoJSON points to H3 hexagons."
    )
    parser.add_argument("geojson_file", type=str, help="Path to the GeoJSON file")
    parser.add_argument("output_file", type=str, help="Path to save the output file")
    parser.add_argument(
        "--output_format",
        type=str,
        default="geojson",
        choices=["geojson", "csv"],
        help="Output file format",
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=8,
        help="H3 resolution (0-15, default: 8)",
    )
    args = parser.parse_args()

    # Convert GeoJSON points to H3 hexagons and save to the output file
    convert_to_h3(
        args.geojson_file, args.output_file, args.output_format, args.resolution
    )
