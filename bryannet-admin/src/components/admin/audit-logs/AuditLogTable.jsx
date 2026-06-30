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

import AuditLogStatusChip from "./AuditLogStatusChip";

export default function AuditLogTable({
  logs,
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
            <TableCell>User</TableCell>
            <TableCell>Module</TableCell>
            <TableCell>Action</TableCell>
            <TableCell>Target</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="center">
              Details
            </TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {logs.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={7}
                align="center"
                sx={{ py: 6 }}
              >
                <Typography color="text.secondary">
                  No audit logs found.
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            logs.map((log) => (
              <TableRow
                key={log.id}
                hover
              >
                <TableCell>
                  {log.timestamp}
                </TableCell>

                <TableCell>
                  {log.user}
                </TableCell>

                <TableCell>
                  {log.module}
                </TableCell>

                <TableCell>
                  {log.action}
                </TableCell>

                <TableCell>
                  {log.target}
                </TableCell>

                <TableCell>
                  <AuditLogStatusChip
                    status={log.status}
                  />
                </TableCell>

                <TableCell align="center">
                  <Tooltip title="View Details">
                    <IconButton
                      onClick={() => onView(log)}
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