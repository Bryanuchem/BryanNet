import Chip from "@mui/material/Chip";

const registrationStepConfig = {
    START: {
        label: "Started",
        color: "info",
    },

    NAME: {
        label: "Awaiting Name",
        color: "warning",
    },

    PHONE: {
        label: "Awaiting Phone",
        color: "warning",
    },

    COMPLETE: {
        label: "Complete",
        color: "success",
    },
};

function BadgeChip({
    label,
    color = "default",
    variant,
    value,
}) {
    if (variant === "registrationStep") {
        const config =
            registrationStepConfig[value] || {
                label: value,
                color: "default",
            };

        return (
            <Chip
                label={config.label}
                color={config.color}
                size="small"
            />
        );
    }

    return (
        <Chip
            label={label}
            color={color}
            size="small"
        />
    );
}

export default BadgeChip;