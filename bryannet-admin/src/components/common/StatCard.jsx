import {
    Avatar,
    Paper,
    Skeleton,
    Stack,
    Typography,
} from "@mui/material";

import { alpha } from "@mui/material/styles";

function StatCard({
    title,
    value,
    icon,
    loading = false,
    color = "primary",
}) {

    return (

        <Paper
            elevation={0}
            sx={(theme) => ({
                height: "100%",
                minHeight: 170,
                borderRadius: 3,
                border: 1,
                borderColor: alpha(
                    theme.palette[color].main,
                    0.25
                ),
                bgcolor: alpha(
                    theme.palette[color].main,
                    0.10
                ),
                transition: "all 0.2s ease-in-out",

                "&:hover": {
                    transform: "translateY(-3px)",
                    boxShadow: theme.shadows[5],
                },
            })}
        >

            <Stack
                justifyContent="space-between"
                alignItems="center"
                sx={{
                    height: "100%",
                    py: 3,
                    px: 3,
                }}
            >

                <Stack
                    direction="row"
                    spacing={1.25}
                    justifyContent="center"
                    alignItems="center"
                >

                    <Avatar
                        sx={(theme) => ({
                            width: 48,
                            height: 48,
                            borderRadius: 2,
                            bgcolor: alpha(
                                theme.palette[color].main,
                                0.20
                            ),
                            color: theme.palette[color].main,
                        })}
                    >
                        {icon}
                    </Avatar>

                    <Typography
                        variant="subtitle2"
                        align="center"
                        sx={{
                            fontWeight: 700,
                            textTransform: "uppercase",
                            letterSpacing: 1,
                            color: "text.secondary",
                        }}
                    >
                        {title}
                    </Typography>

                </Stack>

                {loading ? (

                    <Skeleton
                        variant="text"
                        width={120}
                        height={60}
                    />

                ) : (

                    <Stack
                        justifyContent="center"
                        alignItems="center"
                        sx={{
                            flexGrow: 1,
                            width: "100%",
                        }}
                    >

                        <Typography
                            variant="h3"
                            align="center"
                            sx={{
                                width: "100%",
                                fontWeight: 700,
                                lineHeight: 1,
                            }}
                        >
                            {value}
                        </Typography>

                    </Stack>

                )}

            </Stack>

        </Paper>

    );

}

export default StatCard;