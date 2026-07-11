import SettingsIcon from "@mui/icons-material/Settings";
import TuneIcon from "@mui/icons-material/Tune";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import NotificationsIcon from "@mui/icons-material/Notifications";
import LanIcon from "@mui/icons-material/Lan";
import PaymentsIcon from "@mui/icons-material/Payments";
import HubIcon from "@mui/icons-material/Hub";
import BrandingWatermarkIcon from "@mui/icons-material/BrandingWatermark";
import StorageIcon from "@mui/icons-material/Storage";

const settingsNavigation = {
  id: "settings",
  title: "Settings",
  icon: SettingsIcon,
  children: [

      {

          id: "settings-general",

          title: "General",

          path: "/settings/general",

          icon: TuneIcon,

          permission: "settings.general",

      },

      {

          id: "settings-authentication",

          title: "Authentication",

          path: "/settings/authentication",

          icon: AdminPanelSettingsIcon,

          permission: "settings.authentication",

      },

      {

          id: "settings-notifications",

          title: "Notifications",

          path: "/settings/notifications",

          icon: NotificationsIcon,

          permission: "settings.notifications",

      },

      {

          id: "settings-network",

          title: "Network",

          path: "/settings/network",

          icon: LanIcon,

          permission: "settings.network",

      },

      {

          id: "settings-billing",

          title: "Billing",

          path: "/settings/billing",

          icon: PaymentsIcon,

          permission: "settings.billing",

      },

      {

          id: "settings-integrations",

          title: "Integrations",

          path: "/settings/integrations",

          icon: HubIcon,

          permission: "settings.integrations",

      },

      {

          id: "settings-branding",

          title: "Branding",

          path: "/settings/branding",

          icon: BrandingWatermarkIcon,

          permission: "settings.branding",

      },

      {

          id: "settings-system",

          title: "System",

          path: "/settings/system",

          icon: StorageIcon,

          permission: "settings.system",

      },

  ]
};

export default settingsNavigation;