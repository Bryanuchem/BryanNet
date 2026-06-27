import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

function SidebarBrand() {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight="bold">
                BryanNet
            </Typography>

            <Typography
                variant="body2"
                color="rgba(255,255,255,.7)"
            >
                ISP Platform
            </Typography>
        </Box>
    );
}

export default SidebarBrand;