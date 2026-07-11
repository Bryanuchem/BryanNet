import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";

import SearchIcon from "@mui/icons-material/Search";

function SearchBar({
    value,
    onChange,
    placeholder = "Search...",
    sx,
}) {
    return (
        <TextField
            fullWidth
            size="small"
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            sx={{
                ...sx,
            }}
            InputProps={{
                startAdornment: (
                    <InputAdornment position="start">
                        <SearchIcon />
                    </InputAdornment>
                ),
            }}
        />
    );
}

export default SearchBar;