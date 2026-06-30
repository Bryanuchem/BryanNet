import {
  Checkbox,
  FormControlLabel,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

export default function PermissionCheckbox({
  permission,
  groupId,
  onChange,
}) {
  const handleChange = (event) => {
    onChange?.({
      groupId,
      permissionId: permission.id,
      checked: event.target.checked,
    });
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        height: "100%",
        borderRadius: 2,
      }}
    >
      <Stack spacing={0.5}>
        <FormControlLabel
          control={
            <Checkbox
              checked={permission.enabled}
              onChange={handleChange}
            />
          }
          label={
            <Typography fontWeight={500}>
              {permission.name}
            </Typography>
          }
        />

        {permission.description && (
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{ pl: 4.5 }}
          >
            {permission.description}
          </Typography>
        )}
      </Stack>
    </Paper>
  );
}