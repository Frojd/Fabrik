# Project layout

We use the following project layout when deploying (it follows the same pattern as the ruby tool capistrano).

```
┌─────────────┐                            
│  releases   │─┐                          
└─────────────┘ │  ┌───────────────────┐   
                ├─▶│   201504121255    │──┐
                │  └───────────────────┘  │
                │  ┌───────────────────┐  │
                └─▶│   201504121213    │  │
                   └───────────────────┘  │
┌─────────────┐                           │
│   current   │─┬─────────────────────────┘
└─────────────┘ │  ┌───────────────────┐   
                ├─▶│     myapp.py      │   
                │  └───────────────────┘   
                │  ┌───────────────────┐   
                └─▶│      urls.py      │   
                   └───────────────────┘   
                   ┌───────────────────┐   
                   │       .env        │◀─┐
                   └───────────────────┘  │
┌─────────────┐                           │
│   shared    │─┐                         │
└─────────────┘ │  ┌──────────────────┐   │
                └─▶│       .env       │───┘
                   └──────────────────┘    
```
