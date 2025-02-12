import arcpy

arcpy.env.overwriteOutput = True


class CalculateSinuosity(object):
    def __init__(self):
        self.label = "Calculate Sinuosity"
        self.description = (
            "Sinuosity measures the amount that a river meanders within its valley, "
            "calculated by dividing total stream length by valley length."
        )
        self.category = "Sinuosity"

    def getParameterInfo(self):
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        in_features.filter.list = ["Polyline"]

        sinuosity_field = arcpy.Parameter(
            displayName="Sinuosity Field",
            name="sinuosity_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input",
        )
        sinuosity_field.value = "sinuosity"

        out_features = arcpy.Parameter(
            displayName="Output Features",
            name="out_features",
            datatype="DEFeatureClass",
            parameterType="Derived",
            direction="Output"
        )
        out_features.parameterDependencies = [in_features.name]
        out_features.schema.clone = True

        parameters = [in_features, sinuosity_field, out_features]
        return parameters

    def isLicensed(self):
        """Check if the user is licensed to run this tool."""
        return True

    def updateParameters(self, parameters):
        """Update parameters dynamically based on input."""
        if parameters[0].altered:
            parameters[1].value = arcpy.ValidateFieldName(parameters[1].value, parameters[0].value)
        return

    def updateMessages(self, parameters):
        """Validate inputs and show messages if necessary."""
        return

    def execute(self, parameters, messages):
        from ...tools.calculate_sinuosity import main
        """Main execution method."""
        main(parameters[0].valueAsText, parameters[1].valueAsText)
