import {
    Box,
    Button,
    Typography,
} from "@mui/material";

function PageHeader({
    title,
    subtitle,
    actionLabel,
    actionIcon,
    onAction,
}) {
    return (
        <Box sx={{ mb: 4 }}>
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

            {actionLabel && (
                <Button
                    variant="contained"
                    startIcon={actionIcon}
                    onClick={onAction}
                    sx={{ mt: 3 }}
                >
                    {actionLabel}
                </Button>
            )}
        </Box>
    );
}

export default PageHeader;