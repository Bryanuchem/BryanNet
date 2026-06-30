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

import AuditLogStatusChip from "./AuditLogStatusChip";

export default function AuditLogDetailsDialog({
  open,
  log,
  onClose,
}) {
  if (!log) {
    return null;
  }

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="md"
    >
      <DialogTitle>Audit Log Details</DialogTitle>

      <DialogContent dividers>
        <Stack spacing={3}>
          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Activity Information
            </Typography>

            <Stack spacing={2}>
              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Timestamp
                </Typography>

                <Typography>{log.timestamp}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  User
                </Typography>

                <Typography>{log.user}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Module
                </Typography>

                <Typography>{log.module}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Action
                </Typography>

                <Typography>{log.action}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Target
                </Typography>

                <Typography>{log.target}</Typography>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  Status
                </Typography>

                <Box mt={1}>
                  <AuditLogStatusChip
                    status={log.status}
                  />
                </Box>
              </Box>

              <Box>
                <Typography
                  variant="caption"
                  color="text.secondary"
                >
                  IP Address
                </Typography>

                <Typography>{log.ipAddress}</Typography>
              </Box>
            </Stack>
          </Box>

          <Divider />

          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Description
            </Typography>

            <Typography color="text.secondary">
              {log.description}
            </Typography>
          </Box>

          <Divider />

          <Box>
            <Typography
              variant="h6"
              gutterBottom
            >
              Payload (Placeholder)
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
{JSON.stringify(log, null, 2)}
              </pre>
            </Box>
          </Box>
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}