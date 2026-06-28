import {
    Box,
    Button,
    Typography,
} from "@mui/material";

import InboxIcon from "@mui/icons-material/Inbox";

function EmptyState({
    title = "Nothing here yet",
    description = "There's nothing to display.",
    buttonText,
    onButtonClick,
}) {
    return (
        <Box
            sx={{
                py: 8,
                px: 3,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                textAlign: "center",
            }}
        >
            <InboxIcon
                sx={{
                    fontSize: 72,
                    color: "grey.400",
                    mb: 2,
                }}
            />

            <Typography
                variant="h6"
                fontWeight={700}
            >
                {title}
            </Typography>

            <Typography
                color="text.secondary"
                sx={{
                    mt: 1,
                    maxWidth: 420,
                }}
            >
                {description}
            </Typography>

            {buttonText && (
                <Button
                    variant="contained"
                    sx={{ mt: 4 }}
                    onClick={onButtonClick}
                >
                    {buttonText}
                </Button>
            )}
        </Box>
    );
}

export default EmptyState;