import {
    Paper,
    Typography,
} from "@mui/material";

function DashboardSection({
    title,
    header,
    action,
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

                <div

                    style={{

                        display: "flex",

                        justifyContent: "space-between",

                        alignItems: "center",

                        marginBottom: 24,

                    }}

                >

                    <Typography

                        variant="h6"

                        fontWeight={600}

                    >

                        {title}

                    </Typography>

                    {action}

                </div>

            )}

            {children}

        </Paper>

    );

}

export default DashboardSection;