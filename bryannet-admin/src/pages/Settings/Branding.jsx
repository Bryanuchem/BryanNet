import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import CompanyBrandingCard from "../../components/settings/branding/CompanyBrandingCard";
import BrandingAssetsCard from "../../components/settings/branding/BrandingAssetsCard";
import ThemeColorsCard from "../../components/settings/branding/ThemeColorsCard";

const initialSettings = {
  companyName: "BryanNet",
  companyTagline: "Reliable Internet. Exceptional Service.",
  website: "https://www.bryannet.com",
  supportEmail: "support@bryannet.com",

  companyLogo: "bryannet-logo.png",
  favicon: "favicon.ico",
  loginBackground: "login-background.jpg",

  primaryColor: "#1976d2",
  secondaryColor: "#9c27b0",
  accentColor: "#ff9800",
};

export default function Branding() {
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
    console.log("Saving Branding Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Branding Settings"
        subtitle="Configure the visual identity of the BryanNet ISP Platform."
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
        <CompanyBrandingCard
          settings={settings}
          onChange={handleChange}
        />

        <BrandingAssetsCard
          settings={settings}
          onChange={handleChange}
        />

        <ThemeColorsCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}