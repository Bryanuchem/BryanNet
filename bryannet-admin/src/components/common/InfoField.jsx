import {
    Box,
    Stack,
    Typography,
} from "@mui/material";

function InfoField({
    icon,
    label,
    value,
    children,
}) {
    return (
        <Stack
            direction="row"
            spacing={2}
            alignItems="flex-start"
        >
            <Box
                sx={{
                    color: "primary.main",
                    mt: 0.5,
                }}
            >
                {icon}
            </Box>

            <Box sx={{ flex: 1 }}>
                <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{
                        display: "block",
                        fontWeight: 600,
                        letterSpacing: 0.4,
                        mb: 0.5,
                    }}
                >
                    {label}
                </Typography>

                {children ? (
                    children
                ) : (
                    <Typography
                        variant="body1"
                        fontWeight={500}
                    >
                        {value}
                    </Typography>
                )}
            </Box>
        </Stack>
    );
}

export default InfoField;