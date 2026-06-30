import { Chip } from "@mui/material";

const statusConfig = {
  Success: {
    color: "success",
    label: "Success",
  },
  Warning: {
    color: "warning",
    label: "Warning",
  },
  Failed: {
    color: "error",
    label: "Failed",
  },
};

export default function AuditLogStatusChip({ status }) {
  const config = statusConfig[status] ?? {
    color: "default",
    label: status,
  };

  return (
    <Chip
      label={config.label}
      color={config.color}
      size="small"
      variant="filled"
    />
  );
}