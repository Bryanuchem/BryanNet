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
import LogoutIcon from "@mui/icons-material/Logout";

import SessionStatusChip from "./SessionStatusChip";

export default function LoginSessionsTable({
  sessions,
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
            <TableCell>User</TableCell>
            <TableCell>Device</TableCell>
            <TableCell>Browser</TableCell>
            <TableCell>IP Address</TableCell>
            <TableCell>Login Time</TableCell>
            <TableCell>Last Activity</TableCell>
            <TableCell>Status</TableCell>
            <TableCell align="center">
              Actions
            </TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {sessions.length === 0 ? (
            <TableRow>
              <TableCell
                colSpan={8}
                align="center"
                sx={{ py: 6 }}
              >
                <Typography color="text.secondary">
                  No login sessions found.
                </Typography>
              </TableCell>
            </TableRow>
          ) : (
            sessions.map((session) => (
              <TableRow
                key={session.id}
                hover
              >
                <TableCell>
                  {session.user}
                </TableCell>

                <TableCell>
                  {session.device}
                </TableCell>

                <TableCell>
                  {session.browser}
                </TableCell>

                <TableCell>
                  {session.ipAddress}
                </TableCell>

                <TableCell>
                  {session.loginTime}
                </TableCell>

                <TableCell>
                  {session.lastActivity}
                </TableCell>

                <TableCell>
                  <SessionStatusChip
                    status={session.status}
                  />
                </TableCell>

                <TableCell align="center">
                  <Tooltip title="View Session">
                    <IconButton
                      onClick={() => onView(session)}
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </Tooltip>

                  <Tooltip title="Terminate Session">
                    <IconButton color="error">
                      <LogoutIcon />
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