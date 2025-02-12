import arcpy
import math

arcpy.env.overwriteOutput = True


def calculate_sinuosity_value(shape):
    """Calculate sinuosity for a single feature."""
    path_length = shape.length
    straight_distance = math.sqrt(
        (shape.firstPoint.X - shape.lastPoint.X) ** 2 +
        (shape.firstPoint.Y - shape.lastPoint.Y) ** 2
    )
    return path_length / straight_distance if straight_distance > 0 else 1


def calculate_sinuosity(
        feature_class: str,
        field_name: str,
) -> str:
    """Calculate sinuosity for polyline features."""
    existing_fields = [field.name for field in arcpy.ListFields(feature_class)]
    if field_name not in existing_fields:
        arcpy.AddField_management(feature_class, field_name, "DOUBLE")

    with arcpy.da.UpdateCursor(feature_class, [field_name, "SHAPE@"]) as cursor:
        for row in cursor:
            row[0] = calculate_sinuosity_value(row[1])
            cursor.updateRow(row)

    return feature_class


def main(in_features: str, field_name: str = None):
    """Main function to handle sinuosity calculation workflow."""
    if field_name in ["#", "", None]:
        field_name = "sinuosity"

    return calculate_sinuosity(in_features, field_name)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
