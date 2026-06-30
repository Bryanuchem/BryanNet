import SearchIcon from "@mui/icons-material/Search";

import {
  InputAdornment,
  Paper,
  Stack,
  TextField,
} from "@mui/material";

export default function SystemActivityFilters({
  search,
  onSearchChange,
}) {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <Stack
        direction={{
          xs: "column",
          md: "row",
        }}
        spacing={2}
      >
        <TextField
          fullWidth
          placeholder="Search system activity..."
          value={search}
          onChange={(event) =>
            onSearchChange(event.target.value)
          }
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
      </Stack>
    </Paper>
  );
}