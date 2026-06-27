import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import IconButton from "@mui/material/IconButton";
import Avatar from "@mui/material/Avatar";
import { TOPBAR_HEIGHT } from "../../config/layout";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";

function TopBar() {
    return (
        <Box
            sx={{
                height: TOPBAR_HEIGHT,
                bgcolor: "background.paper",
                borderBottom: "1px solid #E5E7EB",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                px: 3,
            }}
        >
            <Typography
                variant="h6"
                fontWeight="bold"
            >
                BryanNet ISP Platform
            </Typography>

            <Stack
                direction="row"
                spacing={2}
                alignItems="center"
            >
                <IconButton>
                    <NotificationsNoneIcon />
                </IconButton>

                <Avatar
                    sx={{
                        width: 36,
                        height: 36,
                    }}
                >
                    A
                </Avatar>
            </Stack>
        </Box>
    );
}

export default TopBar;