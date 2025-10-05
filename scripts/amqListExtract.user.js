// ==UserScript==
// @name         AMQ List Extract
// @version      2.0
// @description  /getList to get all AnnID of your list.
// @description  /getMaster to get the master list.
// @match        https://animemusicquiz.com/*
// @require      https://github.com/Mxyuki/AMQ-Scripts/raw/refs/heads/main/amqDiscretCommand.js
// ==/UserScript==

(function() {
    'use strict';

    // <-- State Management -->
    const animeListState = {
        watching: [],
        completed: [],
        paused: [],
        dropped: [],
        ptw: []
    };

    let masterListId = null;
    let isFetchActive = false;

    // <-- Status Code Mapping -->
    const STATUS_CODES = {
        WATCHING: 1,
        COMPLETED: 2,
        PAUSED: 3,
        DROPPED: 4,
        PLAN_TO_WATCH: 5
    };

    const STATUS_TO_ARRAY = {
        [STATUS_CODES.WATCHING]: 'watching',
        [STATUS_CODES.COMPLETED]: 'completed',
        [STATUS_CODES.PAUSED]: 'paused',
        [STATUS_CODES.DROPPED]: 'dropped',
        [STATUS_CODES.PLAN_TO_WATCH]: 'ptw'
    };

    // <-- Utility Functions -->
    function downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const link = document.createElement('a');

        link.href = URL.createObjectURL(blob);
        link.download = filename;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(link.href);
    }

    function resetAnimeListState() {
        Object.keys(animeListState).forEach(key => {
            animeListState[key] = [];
        });
    }

    function categorizeAnimeList(animeListMap) {
        resetAnimeListState();

        Object.entries(animeListMap).forEach(([animeId, statusCode]) => {
            const arrayKey = STATUS_TO_ARRAY[statusCode];
            if (arrayKey) {
                animeListState[arrayKey].push(Number(animeId));
            }
        });
    }

    // <-- API Functions -->
    function fetchMasterList(masterId) {
        fetch(`https://animemusicquiz.com/libraryMasterList?masterId=${masterId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                downloadJSON(data, 'amqMaster.json');
                gameChat.systemMessage('Master list downloaded successfully');
            })
            .catch(error => {
                console.error('Error fetching master list:', error);
                gameChat.systemMessage('Failed to fetch master list');
            })
            .finally(() => {
                isFetchActive = false;
            });
    }

    function downloadAllAnimeLists() {
        const fileMap = {
            watching: 'amqWatching.json',
            completed: 'amqCompleted.json',
            paused: 'amqPaused.json',
            dropped: 'amqDropped.json',
            ptw: 'amqPTW.json'
        };

        Object.entries(fileMap).forEach(([key, filename]) => {
            downloadJSON(animeListState[key], filename);
        });

        gameChat.systemMessage('Anime lists downloaded successfully');
        isFetchActive = false;
    }

    // <-- Command Registration -->
    window.CommandRegistry.register('/getList', () => {
        isFetchActive = true;
        socket.sendCommand({ type: 'library', command: 'get anime status list' });
    });

    window.CommandRegistry.register('/getMaster', () => {
        isFetchActive = true;
        socket.sendCommand({ type: 'library', command: 'get current master list id' });
    });

    // <-- Event Listeners -->
    new Listener('get anime status list', (payload) => {
        if (!isFetchActive) return;

        categorizeAnimeList(payload.animeListMap);
        downloadAllAnimeLists();
    }).bindListener();

    new Listener('get current master list id', (payload) => {
        if (!isFetchActive) return;

        masterListId = payload.masterListId;

        if (masterListId) {
            fetchMasterList(masterListId);
        } else {
            gameChat.systemMessage('No master list ID found');
            isFetchActive = false;
        }
    }).bindListener();

})();
