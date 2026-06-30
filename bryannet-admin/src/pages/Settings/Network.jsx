import { useState } from "react";
import {
  Box,
  Button,
  Stack,
} from "@mui/material";

import SaveRoundedIcon from "@mui/icons-material/SaveRounded";
import RestartAltRoundedIcon from "@mui/icons-material/RestartAlt";

import PageHeader from "../../components/common/PageHeader";

import NetworkDefaultsCard from "../../components/settings/network/NetworkDefaultsCard";
import IpAddressManagementCard from "../../components/settings/network/IpAddressManagementCard";
import RouterDefaultsCard from "../../components/settings/network/RouterDefaultsCard";

const initialSettings = {
  defaultGateway: "192.168.1.1",
  subnetMask: "255.255.255.0",
  primaryDns: "8.8.8.8",
  secondaryDns: "8.8.4.4",

  addressPool: "192.168.1.100 - 192.168.1.250",
  leaseDuration: "24 Hours",
  dhcpEnabled: true,
  autoAssignAddresses: true,

  defaultRouterName: "BryanNet-Router",
  managementVlan: "10",
  managementInterface: "ether1",
  defaultMtu: "1500",
};

export default function Network() {
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
    console.log("Saving Network Settings", settings);
  };

  return (
    <Box>
      <PageHeader
        title="Network Settings"
        subtitle="Configure default network, IP address management and router settings."
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
        <NetworkDefaultsCard
          settings={settings}
          onChange={handleChange}
        />

        <IpAddressManagementCard
          settings={settings}
          onChange={handleChange}
        />

        <RouterDefaultsCard
          settings={settings}
          onChange={handleChange}
        />
      </Stack>
    </Box>
  );
}