import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";

function SidebarFooter() {
    return (
        <Box sx={{ mt: "auto" }}>
            <Divider
                sx={{
                    borderColor: "rgba(255,255,255,.12)",
                }}
            />

            <Box sx={{ p: 3 }}>
                <Typography fontWeight="bold">
                    Admin
                </Typography>

                <Typography
                    variant="body2"
                    color="rgba(255,255,255,.7)"
                >
                    Super Administrator
                </Typography>
            </Box>
        </Box>
    );
}

export default SidebarFooter;