import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

function PageHeader({ title, subtitle }) {
    return (
        <Box
            sx={{
                mb: 4,
            }}
        >
            <Typography
                variant="h4"
                fontWeight="bold"
            >
                {title}
            </Typography>

            {subtitle && (
                <Typography
                    variant="body1"
                    color="text.secondary"
                    sx={{ mt: 0.5 }}
                >
                    {subtitle}
                </Typography>
            )}
        </Box>
    );
}

export default PageHeader;