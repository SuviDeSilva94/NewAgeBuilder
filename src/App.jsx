import { useState, useEffect, useRef } from 'react';
import SplitPane from 'react-split-pane';
import {
  Box,
  CssBaseline,
  ThemeProvider,
  createTheme,
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Tooltip,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Select, 
  MenuItem, 
  FormControl,
   InputLabel,
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import GitHubIcon from '@mui/icons-material/GitHub';
import BoltIcon from '@mui/icons-material/FlashOn';
import CodeIcon from '@mui/icons-material/Code';

const WS_URL = 'ws://localhost:8000/ws';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#1a1a1a',
      paper: '#2d2d2d',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          margin: 0,
          padding: 0,
          height: '100vh',
          width: '100vw',
          overflow: 'hidden',
        },
        /* Add global resizer styles here */
        '.SplitPane .Resizer': {
          background: '#444',
          opacity: 0.2,
          zIndex: 1,
          boxSizing: 'border-box',
          backgroundClip: 'padding-box',
        },
        '.SplitPane .Resizer:hover': {
          opacity: 0.5,
          transition: 'all 0.2s ease-in-out',
        },
        '.SplitPane .Resizer.vertical': {
          width: '5px',
          margin: '0 -2px',
          cursor: 'col-resize',
        },
      },
    },
  },
});


const filterValidSx = (styleObj = {}) => {
  const invalidKeys = ['content', 'title', 'subtitle', 'children'];
  return Object.fromEntries(
    Object.entries(styleObj).filter(([key]) => !invalidKeys.includes(key))
  );
};

function App() {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'ai',
      content:
        "\uD83D\uDC4B Hi! I'm NewAgeBuilder, your AI Web builder.\n\nYou can give me prompts like:\n- \"Create a hero section with title 'Welcome to NewAgeBuilder'\"\n- \"Add 3 cards for stats: Pre-Orders, Available Cars, Avg. CIF Value\"\n- \"Insert a table showing sample orders\"\n\nI'll build your webpage section by section. Just type and hit Enter! \uD83D\uDE80",
    },
  ]);
  const [dynamicComponents, setDynamicComponents] = useState([]);

  const [model, setModel] = useState('gemini');

  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => console.log('WebSocket Connected');
    ws.current.onclose = () => console.log('WebSocket Disconnected');
    ws.current.onerror = (error) => console.error('WebSocket Error:', error);

    ws.current.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log('Message from server:', message);

        if (message.action === 'update_component') {
          const components = Array.isArray(message.payload) ? message.payload : [message.payload];
          const isEdit = message.mode === 'edit';
          setDynamicComponents((prev) => (isEdit ? [...components] : [...prev, ...components]));

          setMessages((prev) => [
            ...prev,
            {
              type: 'ai',
              content: message.message || `AI generated ${components.length} component(s).`,
            },
          ]);
        } else if (message.error) {
          console.error('Backend Error:', message.error);
        }
      } catch (e) {
        console.error('Failed to parse message or invalid format:', e);
      }
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const sendPrompt = () => {
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected.');
      return;
    }
    if (prompt.trim() === '') return;

    const message = {
      type: dynamicComponents.length ? 'edit' : 'prompt',
      content: prompt,
      components: dynamicComponents,
      model, // 👈 add model key
    };
    ws.current.send(JSON.stringify(message));
    setMessages((prev) => [...prev, { type: 'user', content: prompt }]);
    setPrompt('');
  };

  // const renderElement = (el, index) => {
  //   if (!el || typeof el !== 'object') return null;

  //   const {
  //     type = 'Box',
  //     props = {},
  //     children,
  //     style = {},
  //     content,
  //     title,
  //     subtitle,
  //   } = el;

  //   const defaultSx = {
  //     p: 4,
  //     mb: 3,
  //     borderRadius: 2,
  //     boxShadow: 3,
  //     textAlign: 'center',
  //     bgcolor: !style?.backgroundColor ? 'background.paper' : undefined,
  //     ...style,
  //   };

  //   return (
  //     <Box key={index} sx={defaultSx} {...props}>
  //       {title && <Typography variant="h5" sx={{ mb: 1 }}>{title}</Typography>}
  //       {subtitle && <Typography variant="subtitle1" sx={{ mb: 2 }}>{subtitle}</Typography>}
  //       {content && <Typography variant="body2">{content}</Typography>}

  //       {Array.isArray(children)
  //         ? children.map((child, i) => renderElement(child, i))
  //         : typeof children === 'string'
  //         ? <Typography>{children}</Typography>
  //         : null}
  //     </Box>
  //   );
  // };

  const renderElement = (el, index) => {
    if (!el || typeof el !== 'object') return null;
  
    const {
      type = 'Box',
      props = {},
      children,
      style = {},
      content,
      title,
      subtitle,
    } = el;
  
    const defaultSx = {
      p: 4,
      mb: 3,
      borderRadius: 2,
      boxShadow: 3,
      textAlign: 'center',
      bgcolor: !style?.backgroundColor ? 'background.paper' : undefined,
      ...filterValidSx(style),
    };
  
    switch (type) {
      case 'Header':
        return (
          <Box key={index} sx={defaultSx} {...props}>
            {el.logo?.src && (
              <img src={el.logo.src} alt={el.logo.alt || 'Logo'} style={{ height: 40, marginBottom: 8 }} />
            )}
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
              {el.navigation?.map((nav, i) => (
                <Button key={i} href={nav.link} sx={{ color: el.style?.textColor || 'white' }}>
                  {nav.label}
                </Button>
              ))}
            </Box>
            {el.callToAction && (
              <Button variant="contained" href={el.callToAction.link} sx={{ mt: 2 }}>
                {el.callToAction.label}
              </Button>
            )}
          </Box>
        );
  
      case 'Hero':
        return (
          <Box key={index} sx={defaultSx}>
            {el.backgroundImage && (
              <Box
                sx={{
                  backgroundImage: `url(${el.backgroundImage})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  borderRadius: 2,
                  height: 300,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  color: '#fff',
                  p: 3,
                  ...filterValidSx(style)
                }}
              >
                <Typography variant="h3" sx={{ mb: 1 }}>{title}</Typography>
                <Typography variant="h6">{subtitle}</Typography>
                {el.callToAction && (
                  <Button
                    href={el.callToAction.link}
                    sx={{ mt: 2, ...el.callToAction.style }}
                  >
                    {el.callToAction.label}
                  </Button>
                )}
              </Box>
            )}
          </Box>
        );
  
      case 'Section':
        if (el.layout === 'grid') {
          return (
            <Box
              key={index}
              sx={{
                ...defaultSx,
                display: 'grid',
                gridTemplateColumns: `repeat(${el.columns || 1}, 1fr)`,
                gap: el.gap || 2,
              }}
            >
              {el.children?.map((child, i) => renderElement(child, i))}
            </Box>
          );
        } else if (el.layout === 'flex') {
          return (
            <Box key={index} sx={{ ...defaultSx, display: 'flex', flexWrap: 'wrap', gap: 2, ...filterValidSx(el.style) }}>
              {el.children?.map((child, i) => renderElement(child, i))}
            </Box>
          );
        } else {
          return (
            <Box key={index} sx={defaultSx}>
              {title && <Typography variant="h5" sx={{ mb: 1 }}>{title}</Typography>}
              {el.description && <Typography variant="body2" sx={{ mb: 2 }}>{el.description}</Typography>}
              {el.items?.map((item, i) => renderElement(item, i))}
              {el.children?.map((child, i) => renderElement(child, i))}
            </Box>
          );
        }
  
      case 'Card':
        return (
          <Box key={index} sx={defaultSx}>
            {el.image && <img src={el.image} alt={el.title} style={{ width: '100%', borderRadius: 8, marginBottom: 8 }} />}
            <Typography variant="h6">{el.title}</Typography>
            <Typography variant="body2">{el.description}</Typography>
          </Box>
        );
  
        case 'Text':
          return (
            <Box key={index} sx={defaultSx}>
              <Typography sx={el.style}>{el.content}</Typography>
            </Box>
          );
        
        case 'Image':
          return (
            <Box key={index} sx={defaultSx}>
              <img
                src={el.src}
                alt={el.alt || 'Image'}
                style={{ maxWidth: '100%', ...el.style }}
              />
            </Box>
          );
      
        case 'ContactForm':
            return (
              <Box key={index} sx={defaultSx}>
                {title && <Typography variant="h5" sx={{ mb: 2 }}>{title}</Typography>}
                <Box component="form" sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {el.fields?.map((field, i) => (
                    <TextField
                      key={i}
                      label={field.label}
                      type={field.type}
                      required={field.required}
                      fullWidth
                      multiline={field.type === 'textarea'}
                      minRows={field.type === 'textarea' ? 3 : undefined}
                    />
                  ))}
                  <Button
                    variant="contained"
                    sx={{ alignSelf: 'flex-start', ...el.cta?.style }}
                  >
                    {el.cta?.label || 'Submit'}
                  </Button>
                </Box>
              </Box>
            );
  
            case 'Table':
              return (
                <Box key={index} sx={defaultSx}>
                  {title && <Typography variant="h6" sx={{ mb: 2 }}>{title}</Typography>}
                  <TableContainer component={Paper}>
                    <Table>
                      <TableHead>
                        <TableRow>
                          {el.columns?.map((col, i) => (
                            <TableCell key={i}>{col}</TableCell>
                          ))}
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {el.rows?.map((row, rowIndex) => (
                          <TableRow key={rowIndex}>
                            {row.map((cell, i) => (
                              <TableCell key={i}>{cell}</TableCell>
                            ))}
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>
              );

      case 'Footer':
        return (
          <Box key={index} sx={{ ...defaultSx, textAlign: 'center' }}>
            <Typography variant="body2">{el.content || el.copyright}</Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 1 }}>
              {el.socialLinks?.map((link, i) => (
                <a key={i} href={link.link || link.href} target="_blank" rel="noopener noreferrer" style={{ color: '#fff' }}>
                  <i className={link.icon}></i>
                </a>
              ))}
            </Box>
          </Box>
        );
  
      default:
        return (
          <Box key={index} sx={defaultSx} {...props}>
            {title && <Typography variant="h5" sx={{ mb: 1 }}>{title}</Typography>}
            {subtitle && <Typography variant="subtitle1" sx={{ mb: 2 }}>{subtitle}</Typography>}
            {content && <Typography variant="body2">{content}</Typography>}
            {Array.isArray(children)
              ? children.map((child, i) => renderElement(child, i))
              : typeof children === 'string'
              ? <Typography>{children}</Typography>
              : null}
          </Box>
        );
    }
  };
  
  
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100vw' }}>
        <AppBar position="fixed" color="transparent" elevation={1} sx={{ zIndex: 1201 }}>
          <Toolbar sx={{ justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Typography sx={{ fontWeight: 600, fontSize: 16 }}>❤️ NewAgeBuilder-Appflow</Typography>
              <Button size="small" variant="outlined" sx={{ textTransform: 'none', color: 'white', borderColor: 'gray' }}>
                Home ▾
              </Button>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Tooltip title="View code"><IconButton><CodeIcon /></IconButton></Tooltip>
              <Tooltip title="Bolt"><IconButton><BoltIcon /></IconButton></Tooltip>
              <Tooltip title="GitHub"><IconButton><GitHubIcon /></IconButton></Tooltip>
              <Button variant="contained">Publish</Button>
            </Box>
          </Toolbar>
        </AppBar>

        <SplitPane split="vertical" defaultSize="50%" style={{ flex: 1, marginTop: '64px' }}>
          {/* Left Side: Chat */}
          <Box sx={{ height: 'calc(100% - 64px)', position: 'relative', display: 'flex', flexDirection: 'column', bgcolor: 'background.paper' }}>
            <Box sx={{ flexGrow: 1, overflowY: 'auto', px: 2, pt: 2, pb: '120px' }}>
              {messages.map((msg, idx) => (
                <Box
                  key={idx}
                  sx={{
                    p: 2,
                    mb: 1,
                    borderRadius: 2,
                    maxWidth: '85%',
                    bgcolor: msg.type === 'user' ? 'primary.main' : 'background.default',
                    ml: msg.type === 'user' ? 'auto' : 0,
                  }}
                >
                  <Typography color={msg.type === 'user' ? 'white' : 'text.primary'} sx={{ whiteSpace: 'pre-line' }}>
                    {msg.content}
                  </Typography>
                </Box>
              ))}
            </Box>

            {/* Floating Input */}
            <Box
              component="form"
              onSubmit={(e) => {
                e.preventDefault();
                sendPrompt();
              }}
              sx={{
                position: 'absolute',
                bottom: 16,
                left: 16,
                right: 16,
                borderRadius: '24px',
                border: '1px solid rgba(255,255,255,0.1)',
                bgcolor: 'background.default',
                display: 'flex',
                alignItems: 'center',
                px: 2,
                py: 1,
                boxShadow: 3,
              }}
            >
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Start typing a prompt..."
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendPrompt();
                  }
                }}
                style={{
                  flexGrow: 1,
                  resize: 'none',
                  border: 'none',
                  outline: 'none',
                  fontSize: '15px',
                  background: 'transparent',
                  color: 'white',
                  fontFamily: 'inherit',
                  padding: '8px 0',
                  lineHeight: '20px',
                }}
              />
              <FormControl
                variant="standard"
                sx={{ minWidth: 100, mr: 2 }}
              >
                <InputLabel sx={{ color: 'white' }}>Model</InputLabel>
                <Select
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  label="Model"
                  sx={{
                    color: 'white',
                    '& .MuiSelect-icon': { color: 'white' },
                    '&::before': { borderBottomColor: 'white' },
                    '&:hover:not(.Mui-disabled)::before': { borderBottomColor: 'white' },
                  }}
                >
                  <MenuItem value="gemini">Gemini</MenuItem>
                  <MenuItem value="openai">GPT-4</MenuItem>
                </Select>
              </FormControl>

              <IconButton
                type="submit"
                sx={{
                  ml: 1,
                  bgcolor: 'primary.main',
                  color: 'white',
                  '&:hover': { bgcolor: 'primary.dark' },
                  width: 36,
                  height: 36,
                }}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              </IconButton>
            </Box>
          </Box>

          {/* Right Side: Dynamic Component Preview */}
          <Box
            sx={{
              height: '100%',
              width: '100%',
              overflow: 'auto',
              bgcolor: 'background.default',
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Typography
              variant="h5"
              sx={{
                mb: 2,
                textAlign: 'center',
                color: 'primary.light', 
                fontWeight: 600
              }}
            >
              AI Generated Preview
            </Typography>
            {dynamicComponents.length === 0 ? (
              <Typography color="text.secondary">Enter a prompt to generate content...</Typography>
            ) : (
              dynamicComponents.map((comp, i) => renderElement(comp, i))
            )}
          </Box>
        </SplitPane>
      </Box>
    </ThemeProvider>
  );
}

export default App;