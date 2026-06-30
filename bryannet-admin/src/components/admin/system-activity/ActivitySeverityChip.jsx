import { Chip } from "@mui/material";

const severityConfig = {
  Info: {
    color: "info",
    label: "Info",
  },
  Success: {
    color: "success",
    label: "Success",
  },
  Warning: {
    color: "warning",
    label: "Warning",
  },
  Critical: {
    color: "error",
    label: "Critical",
  },
};

export default function ActivitySeverityChip({ severity }) {
  const config = severityConfig[severity] ?? {
    color: "default",
    label: severity,
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