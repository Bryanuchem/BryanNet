import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Stack,
  Typography,
} from "@mui/material";

import LogoutIcon from "@mui/icons-material/Logout";

import SessionStatusChip from "./SessionStatusChip";

export default function SessionDetailsDialog({
  open,
  session,
  onClose,
}) {
  if (!session) {
    return null;
  }

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="md"
    >
      <DialogTitle>Session Details</DialogTitle>

      <DialogContent dividers>
        <Stack spacing={3}>
          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Session Information
            </Typography>

            <Stack spacing={2}>
              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Administrator
                </Typography>

                <Typography>{session.user}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Device
                </Typography>

                <Typography>{session.device}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Browser
                </Typography>

                <Typography>{session.browser}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Operating System
                </Typography>

                <Typography>
                  {session.operatingSystem}
                </Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  IP Address
                </Typography>

                <Typography>{session.ipAddress}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Location
                </Typography>

                <Typography>{session.location}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Login Time
                </Typography>

                <Typography>{session.loginTime}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Last Activity
                </Typography>

                <Typography>
                  {session.lastActivity}
                </Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Status
                </Typography>

                <Box mt={1}>
                  <SessionStatusChip
                    status={session.status}
                  />
                </Box>
              </Box>
            </Stack>
          </Box>

          <Divider />

          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Session Metadata (Placeholder)
            </Typography>

            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                bgcolor: "grey.100",
                overflowX: "auto",
                fontFamily: "monospace",
              }}
            >
              <pre
                style={{
                  margin: 0,
                  whiteSpace: "pre-wrap",
                }}
              >
{JSON.stringify(session, null, 2)}
              </pre>
            </Box>
          </Box>
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Close
        </Button>

        <Button
          variant="contained"
          color="error"
          startIcon={<LogoutIcon />}
          onClick={onClose}
        >
          Terminate Session
        </Button>
      </DialogActions>
    </Dialog>
  );
}