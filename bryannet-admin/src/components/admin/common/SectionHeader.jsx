import { Stack, Typography } from "@mui/material";

export default function SectionHeader({
    title,
    subtitle,
    action = null,
    sx = {},
}) {
    return (
        <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="flex-start"
            sx={{ mb: 2, ...sx }}
        >
            <Stack spacing={0.5}>
                <Typography variant="h6">
                    {title}
                </Typography>

                {subtitle && (
                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        {subtitle}
                    </Typography>
                )}
            </Stack>

            {action}
        </Stack>
    );
}