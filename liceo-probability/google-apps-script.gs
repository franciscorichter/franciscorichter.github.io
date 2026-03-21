// ============================================================
// Google Apps Script — Probability Paradoxes Backend
// ============================================================
// SETUP:
// 1. Create a new Google Sheet
// 2. Extensions > Apps Script
// 3. Paste this entire code into Code.gs
// 4. Click Deploy > New deployment
//    - Type: Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 5. Copy the deployment URL
// 6. Paste it into the SCRIPT_URL in index.html
// ============================================================

function doPost(e) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = getOrCreateSheet();
    var data = JSON.parse(e.postData.contents);
    sheet.appendRow([
      new Date().toISOString(),
      data.session || '',
      data.name || '',
      data.paradox || '',
      data.action || '',
      typeof data.value === 'object' ? JSON.stringify(data.value) : String(data.value)
    ]);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Data');
    if (!sheet) {
      return ContentService.createTextOutput('[]')
        .setMimeType(ContentService.MimeType.JSON);
    }

    var session = e.parameter.session || '';
    var rows = sheet.getDataRange().getValues().slice(1); // skip header

    if (session) {
      rows = rows.filter(function(r) { return r[1] === session; });
    }

    var result = rows.map(function(r) {
      return {
        timestamp: r[0],
        session: r[1],
        name: r[2],
        paradox: r[3],
        action: r[4],
        value: r[5]
      };
    });

    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Data');
  if (!sheet) {
    sheet = ss.insertSheet('Data');
    sheet.appendRow(['timestamp', 'session', 'name', 'paradox', 'action', 'value']);
    sheet.setFrozenRows(1);
    sheet.getRange('A1:F1').setFontWeight('bold');
  }
  return sheet;
}
