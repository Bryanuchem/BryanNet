import { Box } from "@mui/material";

function FilterToolbar({
    children,
}) {

    return (

        <Box
            sx={{
                display: "flex",
                alignItems: "stretch",
                flexWrap: "wrap",
                gap: 2,
                width: "100%",
                mb: 2,
            }}
        >

            {children}

        </Box>

    );

}

export default FilterToolbar;