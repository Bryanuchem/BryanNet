import {
    Paper,
    Typography,
} from "@mui/material";

function DashboardSection({
    title,
    header,
    children,
}) {

    return (

        <Paper
            elevation={0}
            sx={{
                p: 3,
                borderRadius: 3,
                border: 1,
                borderColor: "divider",
                height: "100%",
            }}
        >

            {header ? (

                header

            ) : (

                <Typography
                    variant="h6"
                    fontWeight={600}
                    sx={{
                        mb: 3,
                    }}
                >
                    {title}
                </Typography>

            )}

            {children}

        </Paper>

    );

}

export default DashboardSection;