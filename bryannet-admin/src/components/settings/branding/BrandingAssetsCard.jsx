import {
  Button,
  Card,
  CardContent,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

export default function BrandingAssetsCard({
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
            Branding Assets
          </Typography>

          <Grid container spacing={3}>
            <Grid
              size={{
                xs: 12,
                md: 8,
              }}
            >
              <TextField
                fullWidth
                label="Company Logo"
                value={settings.companyLogo}
                onChange={(event) =>
                  onChange(
                    "companyLogo",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
              display="flex"
              alignItems="flex-end"
            >
              <Button
                fullWidth
                variant="outlined"
              >
                Upload Logo
              </Button>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 8,
              }}
            >
              <TextField
                fullWidth
                label="Favicon"
                value={settings.favicon}
                onChange={(event) =>
                  onChange(
                    "favicon",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
              display="flex"
              alignItems="flex-end"
            >
              <Button
                fullWidth
                variant="outlined"
              >
                Upload Favicon
              </Button>
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 8,
              }}
            >
              <TextField
                fullWidth
                label="Login Background Image"
                value={settings.loginBackground}
                onChange={(event) =>
                  onChange(
                    "loginBackground",
                    event.target.value
                  )
                }
              />
            </Grid>

            <Grid
              size={{
                xs: 12,
                md: 4,
              }}
              display="flex"
              alignItems="flex-end"
            >
              <Button
                fullWidth
                variant="outlined"
              >
                Upload Background
              </Button>
            </Grid>
          </Grid>
        </Stack>
      </CardContent>
    </Card>
  );
}