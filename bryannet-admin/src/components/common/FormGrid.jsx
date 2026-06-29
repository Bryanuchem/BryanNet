import {
    Grid,
} from "@mui/material";

function FormGrid({

    children,

    spacing = 2,

    rowSpacing,

    columnSpacing,

    alignItems = "stretch",

    justifyContent = "flex-start",

    sx = {},

}) {

    return (

        <Grid

            container

            spacing={spacing}

            rowSpacing={rowSpacing}

            columnSpacing={columnSpacing}

            alignItems={alignItems}

            justifyContent={justifyContent}

            sx={sx}

        >

            {children}

        </Grid>

    );

}

export default FormGrid;