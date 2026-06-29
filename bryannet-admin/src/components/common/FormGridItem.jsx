import {
    Grid,
} from "@mui/material";

function FormGridItem({

    xs = 12,

    sm,

    md,

    lg,

    xl,

    children,

}) {

    return (

        <Grid

            size={{

                xs,

                sm,

                md,

                lg,

                xl,

            }}

        >

            {children}

        </Grid>

    );

}

export default FormGridItem;