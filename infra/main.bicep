targetScope = 'resourceGroup'

@description('Azure region for the storage account.')
param location string = 'canadacentral'

@description('Full storage account name; it is converted to lowercase and must be globally unique.')
@minLength(3)
@maxLength(24)
param accountName string = 'pavanreddysa'

@description('Tags applied to the storage account.')
param tags object = {
  app: 'campus-cafe'
  env: 'dev'
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: toLower(accountName)
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowSharedKeyAccess: false
    allowBlobPublicAccess: false
  }
}

resource tableService 'Microsoft.Storage/storageAccounts/tableServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource ordersTable 'Microsoft.Storage/storageAccounts/tableServices/tables@2023-05-01' = {
  parent: tableService
  name: 'orders'
}

resource queueService 'Microsoft.Storage/storageAccounts/queueServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource notifyQueue 'Microsoft.Storage/storageAccounts/queueServices/queues@2023-05-01' = {
  parent: queueService
  name: 'notify'
}

resource notifyPoisonQueue 'Microsoft.Storage/storageAccounts/queueServices/queues@2023-05-01' = {
  parent: queueService
  name: 'notify-poison'
}

output storageAccountName string = storageAccount.name
