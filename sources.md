# Sources And Inspiration Notes

## External References

- Home Assistant Energy documentation: `https://www.home-assistant.io/docs/energy/`
- EMHASS documentation: `https://emhass.readthedocs.io/en/latest/`
- EMHASS community thread: `https://community.home-assistant.io/t/emhass-an-energy-management-for-home-assistant/338126`

## Research Takeaways

- Common solar-EV posts focus on PV excess charging: calculate surplus, convert to charging current, smooth sensor noise, and avoid rapid start/stop behavior.
- EMHASS examples usually treat EVs as deferrable loads scheduled against price, PV forecast, and household load forecast.
- Home Assistant's Energy docs frame HA as a unified picture of grid, solar, storage, and device consumption.
- The distinctive angle for this article is not "solar surplus charging" alone. It is the broader operating-system pattern: state normalization, forecast-aware planning, safety ownership, explicit live-enable, allowlisted actuation, and circuit-level verification.

## Local Evidence Used

- `data/current_snapshot.json`: read-only live snapshot from Home Assistant and Node-RED facts.
- `screenshots/evidence-dashboard.png`: generated from the live snapshot.
- `screenshots/node-red-franklin-dashboard-live.png`: live Node-RED Dashboard 2.0 Franklin page.
- `screenshots/node-red-flow-diagram.png`: generated Node-RED flow diagram.
- `screenshots/franklin-state-machine.png`: generated Franklin state-machine diagram.

## Screenshot Limitations

- Home Assistant Lovelace UI requires interactive username/password login. I did not request, read, or store UI credentials.
- Instead, the article uses a generated evidence dashboard built from authenticated API state queries run on the HA host, plus live Node-RED Dashboard screenshots.
- No secret-bearing files or tokens are included in the article assets.
