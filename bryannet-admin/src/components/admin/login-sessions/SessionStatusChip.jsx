import { Chip } from "@mui/material";

const statusConfig = {
  Online: {
    color: "success",
    label: "Online",
  },
  Idle: {
    color: "warning",
    label: "Idle",
  },
  Offline: {
    color: "default",
    label: "Offline",
  },
};

export default function SessionStatusChip({ status }) {
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