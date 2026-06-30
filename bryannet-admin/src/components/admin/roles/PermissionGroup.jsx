import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Grid,
  Stack,
  Typography,
} from "@mui/material";

import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

import PermissionCheckbox from "./PermissionCheckbox";

export default function PermissionGroup({
  group,
  onPermissionChange,
}) {
  return (
    <Accordion
      disableGutters
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 2,
        "&::before": {
          display: "none",
        },
        "&:not(:last-child)": {
          mb: 2,
        },
      }}
    >
      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
        <Box>
          <Typography variant="subtitle1" fontWeight={600}>
            {group.name}
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            {group.description}
          </Typography>
        </Box>
      </AccordionSummary>

      <AccordionDetails>
        <Grid container spacing={2}>
          {group.permissions.map((permission) => (
            <Grid
              key={permission.id}
              size={{
                xs: 12,
                sm: 6,
                md: 4,
              }}
            >
              <PermissionCheckbox
                permission={permission}
                groupId={group.id}
                onChange={onPermissionChange}
              />
            </Grid>
          ))}
        </Grid>
      </AccordionDetails>
    </Accordion>
  );
}