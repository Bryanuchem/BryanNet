import {
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";

import ActivitySeverityChip from "./ActivitySeverityChip";
import ActivityStatusChip from "./ActivityStatusChip";

export default function SystemActivityTable({
  activities,
  onView,
}) {
  return (
    <TableContainer
      component={Paper}
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Timestamp</TableCell>
            <TableCell>Event</TableCell>
            <TableCell>Module</TableCell>
            <TableCell>Severity</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Source</TableCell>
            <TableCell align="center">
              Details
            </TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {activities.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={7}
                align="center"
                sx={{ py: 6 }}
              >
                <Typography color="text.secondary">
                  No system activity found.
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            activities.map((activity) => (
              <TableRow
                key={activity.id}
                hover
              >
                <TableCell>
                  {activity.timestamp}
                </TableCell>

                <TableCell>
                  {activity.event}
                </TableCell>

                <TableCell>
                  {activity.module}
                </TableCell>

                <TableCell>
                  <ActivitySeverityChip
                    severity={activity.severity}
                  />
                </TableCell>

                <TableCell>
                  <ActivityStatusChip
                    status={activity.status}
                  />
                </TableCell>

                <TableCell>
                  {activity.source}
                </TableCell>

                <TableCell align="center">
                  <Tooltip title="View Details">
                    <IconButton
                      onClick={() => onView(activity)}
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}