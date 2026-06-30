import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import PlatformInformationCard from "../../components/settings/general/PlatformInformationCard";
import RegionalSettingsCard from "../../components/settings/general/RegionalSettingsCard";
import OrganizationDetailsCard from "../../components/settings/general/OrganizationDetailsCard";

const initialSettings = {
  platformName: "BryanNet ISP Platform",
  platformDescription:
    "ISP Management and Customer Administration Platform",

  companyName: "BryanNet",
  companyEmail: "admin@bryannet.com",
  companyPhone: "+234 800 000 0000",

  timeZone: "Africa/Lagos",
  language: "English",
  dateFormat: "DD/MM/YYYY",
  timeFormat: "24 Hour",
  currency: "NGN",

  address: "123 BryanNet Avenue",
  city: "Asaba",
  state: "Delta",
  country: "Nigeria",
  postalCode: "320001",
};

export default function General() {
  const [settings, setSettings] = useState(initialSettings);

  const handleChange = (field, value) => {
    setSettings((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  const handleReset = () => {
    setSettings(initialSettings);
  };

  const handleSave = () => {
    // Placeholder
    console.log("Saving General Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="General Settings"
        subtitle="Manage the basic configuration of the BryanNet ISP Platform."
        actions={
          <Stack direction="row" spacing={2}>
            <Button
              variant="outlined"
              startIcon={<RestartAltRoundedIcon />}
              onClick={handleReset}
            >
              Reset
            </Button>

            <Button
              variant="contained"
              startIcon={<SaveRoundedIcon />}
              onClick={handleSave}
            >
              Save Changes
            </Button>
          </Stack>
        }
      />

      <Stack spacing={3}>
        <PlatformInformationCard
          settings={settings}
          onChange={handleChange}
        />

        <RegionalSettingsCard
          settings={settings}
          onChange={handleChange}
        />

        <OrganizationDetailsCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}