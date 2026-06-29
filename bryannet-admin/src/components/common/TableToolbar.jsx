import {
    Box,
    Button,
    MenuItem,
    Stack,
    TextField,
} from "@mui/material";

import RefreshIcon from "@mui/icons-material/Refresh";
import ClearIcon from "@mui/icons-material/Clear";

function TableToolbar({
    search = "",
    onSearchChange,
    filter = "all",
    onFilterChange,
    filters = [],
    searchPlaceholder = "Search...",
    onRefresh,
    onClear,
}) {
    return (
        <Stack
            direction={{
                xs: "column",
                md: "row",
            }}
            spacing={2}
            justifyContent="space-between"
            alignItems={{
                xs: "stretch",
                md: "center",
            }}
            sx={{
                mb: 2,
            }}
        >
            <Box
                sx={{
                    flex: 1,
                }}
            >
                <TextField
                    fullWidth
                    size="small"
                    placeholder={searchPlaceholder}
                    value={search}
                    onChange={(event) =>
                        onSearchChange(
                            event.target.value
                        )
                    }
                />
            </Box>

            <Stack
                direction="row"
                spacing={1}
                alignItems="center"
            >
                <TextField
                    select
                    size="small"
                    value={filter}
                    onChange={(event) =>
                        onFilterChange(
                            event.target.value
                        )
                    }
                    sx={{
                        minWidth: 180,
                    }}
                >
                    {filters.map((option) => (
                        <MenuItem
                            key={option.value}
                            value={option.value}
                        >
                            {option.label}
                        </MenuItem>
                    ))}
                </TextField>

                <Button
                    variant="outlined"
                    startIcon={<RefreshIcon />}
                    onClick={onRefresh}
                >
                    Refresh
                </Button>

                <Button
                    variant="outlined"
                    color="inherit"
                    startIcon={<ClearIcon />}
                    onClick={onClear}
                >
                    Clear
                </Button>
            </Stack>
        </Stack>
    );
}

export default TableToolbar;