import {
  Card,
  CardContent,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function CompanyBrandingCard({
  settings,
  onChange,
}) {
  return (
    <Card
      elevation={0}
      sx={{
        border: (theme) => `1px solid ${theme.palette.divider}`,
        borderRadius: 3,
      }}
    >
      <CardContent>
        <Stack spacing={3}>
          <Typography variant="h6">
            Company Branding
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Company Name"
                value={settings.companyName}
                onChange={(event) =>
                  onChange(
                    "companyName",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Company Tagline"
                value={settings.companyTagline}
                onChange={(event) =>
                  onChange(
                    "companyTagline",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                label="Website"
                value={settings.website}
                onChange={(event) =>
                  onChange(
                    "website",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 6,
              }}
            >
              <TextField
                fullWidth
                type="email"
                label="Support Email"
                value={settings.supportEmail}
                onChange={(event) =>
                  onChange(
                    "supportEmail",
                    event.target.value
                  )
                }
              />
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}