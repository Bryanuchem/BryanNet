import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";

import SearchIcon from "@mui/icons-material/Search";

function SearchBar({
    value,
    onChange,
    placeholder = "Search...",
}) {
    return (
        <TextField
            fullWidth
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            sx={{ mb: 3 }}
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