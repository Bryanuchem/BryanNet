import { Chip } from "@mui/material";

const statusConfig = {
  Success: {
    color: "success",
    label: "Success",
  },
  Failed: {
    color: "error",
    label: "Failed",
  },
  Pending: {
    color: "warning",
    label: "Pending",
  },
  Running: {
    color: "info",
    label: "Running",
  },
};

export default function ActivityStatusChip({ status }) {
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