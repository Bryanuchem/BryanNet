import {
    Box,
    Typography,
} from "@mui/material";

function PageHeader({
    title,
    subtitle,
    actions = null,
}) {

    return (

        <Box
            sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                flexWrap: "wrap",
                gap: 2,
                mb: 4,
            }}
        >

            <Box>

                <Typography
                    variant="h4"
                    fontWeight={700}
                >
                    {title}
                </Typography>

                {subtitle && (

                    <Typography
                        variant="body1"
                        color="text.secondary"
                        sx={{
                            mt: 0.5,
                        }}
                    >
                        {subtitle}
                    </Typography>

                )}

            </Box>

            {actions && (

                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1.5,
                    }}
                >

                    {actions}

                </Box>

            )}

        </Box>

    );

}

export default PageHeader;