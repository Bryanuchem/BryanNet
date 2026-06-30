import {
    Card,
    CardActionArea,
    CardContent,
    Stack,
    Typography,
    Box,
} from "@mui/material";
import ArrowForwardRoundedIcon from "@mui/icons-material/ArrowForwardRounded";

export default function AdministrationModuleCard({
    title,
    description,
    icon,
    onClick,
}) {
    return (
        <Card
            elevation={1}
            sx={{
                height: "100%",
            }}
        >
            <CardActionArea
                onClick={onClick}
                sx={{
                    height: "100%",
                }}
            >
                <CardContent
                    sx={{
                        height: "100%",
                    }}
                >
                    <Stack
                        spacing={3}
                        sx={{ height: "100%" }}
                    >
                        <Stack
                            direction="row"
                            justifyContent="space-between"
                            alignItems="center"
                        >
                            <Box>{icon}</Box>

                            <ArrowForwardRoundedIcon
                                color="action"
                                fontSize="small"
                            />
                        </Stack>

                        <Box sx={{ flexGrow: 1 }}>
                            <Typography
                                variant="h6"
                                gutterBottom
                            >
                                {title}
                            </Typography>

                            <Typography
                                variant="body2"
                                color="text.secondary"
                            >
                                {description}
                            </Typography>
                        </Box>
                    </Stack>
                </CardContent>
            </CardActionArea>
        </Card>
    );
}