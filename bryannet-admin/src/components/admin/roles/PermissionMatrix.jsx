import {
  Box,
  Card,
  CardContent,
  Divider,
  Stack,
  Typography,
} from "@mui/material";

import PermissionGroup from "./PermissionGroup";

export default function PermissionMatrix({
  permissions = [],
  onPermissionChange,
}) {
  return (
    <Card
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <CardContent>
        <Stack spacing={3}>
          <Box>
            <Typography variant="h6">
              Permissions
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
            >
              Configure what users assigned to this role are allowed to access.
            </Typography>
          </Box>

          <Divider />

          <Stack spacing={3}>
            {permissions.map((group) => (
              <PermissionGroup
                key={group.id}
                group={group}
                onPermissionChange={onPermissionChange}
              />
            ))}
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  );
}